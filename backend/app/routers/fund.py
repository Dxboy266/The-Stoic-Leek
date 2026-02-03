"""
基金数据路由 - 获取基金实时估值
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel

from ..services.fund import fetch_fund_realtime, batch_fetch_funds, search_fund_by_name
from ..services.ocr import recognize_funds_from_screenshot, FundFromOCR


router = APIRouter(prefix="/fund", tags=["基金数据"])


class FundSearchResult(BaseModel):
    """基金搜索结果"""
    code: str
    name: str
    type: str

@router.get("/search/query", response_model=List[FundSearchResult])
async def search_fund(q: str):
    """
    通过名称搜索基金
    """
    if not q:
        return []
        
    results = await search_fund_by_name(q)
    return [FundSearchResult(**r) for r in results]


class FundRealtimeData(BaseModel):
    """基金实时数据"""
    code: str
    name: str
    gsz: float        # 实时估值
    gszzl: float      # 涨跌幅%
    dwjz: float       # 昨日净值
    gztime: str       # 估值时间
    jzrq: str         # 净值日期


class ScreenshotImportRequest(BaseModel):
    """截图导入请求"""
    image: str  # Base64 编码的图片
    # API 配置（从前端传入）
    baseUrl: Optional[str] = None
    apiKey: Optional[str] = None
    model: Optional[str] = None


class ScreenshotImportResponse(BaseModel):
    """截图导入响应"""
    success: bool
    funds: List[FundFromOCR]
    message: str


@router.get("/{code}", response_model=Optional[FundRealtimeData])
async def get_fund_realtime(code: str):
    """
    获取单个基金的实时估值数据
    
    - **code**: 6位基金代码，如 110022
    """
    if not code or len(code) != 6:
        raise HTTPException(status_code=400, detail="请输入6位基金代码")
    
    data = await fetch_fund_realtime(code)
    
    if not data:
        raise HTTPException(status_code=404, detail="基金代码无效或暂无数据")
    
    return FundRealtimeData(**data)


@router.get("/batch/query")
async def get_funds_batch(
    codes: str = Query(..., description="基金代码，逗号分隔，如 110022,519069")
):
    """
    批量获取多个基金的实时估值数据
    """
    code_list = [c.strip() for c in codes.split(",") if c.strip()]
    
    if not code_list:
        raise HTTPException(status_code=400, detail="请提供基金代码")
    
    if len(code_list) > 20:
        raise HTTPException(status_code=400, detail="最多支持20个基金")
    
    results = await batch_fetch_funds(code_list)
    
    return [FundRealtimeData(**item) for item in results]


@router.post("/import/screenshot", response_model=ScreenshotImportResponse)
async def import_from_screenshot(request: ScreenshotImportRequest):
    """
    从截图识别并导入基金持仓
    
    上传支付宝/天天基金的持仓页面截图，自动识别基金信息
    """
    print(f"收到截图导入请求，长度: {len(request.image) if request.image else 0}, 模型: {request.model}")
    if not request.image:
        raise HTTPException(status_code=400, detail="请提供截图")
    
    try:
        funds = await recognize_funds_from_screenshot(
            image_base64=request.image,
            base_url=request.baseUrl,
            api_key=request.apiKey,
            model=request.model
        )
        
        if not funds:
            return ScreenshotImportResponse(
                success=False,
                funds=[],
                message="未能识别出基金信息，请确保截图清晰且包含持仓页面"
            )
        
        return ScreenshotImportResponse(
            success=True,
            funds=funds,
            message=f"成功识别 {len(funds)} 只基金"
        )
    except ImportError as e:
        raise HTTPException(
            status_code=500, 
            detail="AI 视觉模块未安装，请运行: pip install openai"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"识别失败: {str(e)}")
