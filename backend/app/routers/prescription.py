"""
处方路由 - 生成韭菜处方
"""

from fastapi import APIRouter, HTTPException, status

from ..schemas import (
    GeneratePrescriptionRequest, 
    GeneratePrescriptionResponse
)
from ..services import generate_prescription

router = APIRouter(prefix="/prescription", tags=["处方"])


@router.post("/generate", response_model=GeneratePrescriptionResponse)
async def generate(request: GeneratePrescriptionRequest):
    """
    生成韭菜处方 (无需登录)
    
    根据用户输入的盈亏金额和本金，调用 AI 生成运动处方和毒舌建议
    """
    try:
        result = await generate_prescription(
            amount=request.amount,
            total_assets=request.total_assets,
            api_key=request.api_key,
            model=request.model,
            exercises=request.exercises if request.exercises else None
        )
        
        return GeneratePrescriptionResponse(**result)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Server Error: {str(e)}") # 简单的日志
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成失败: {str(e)}"
        )


@router.post("/generate-anonymous", response_model=GeneratePrescriptionResponse)
async def generate_anonymous(request: GeneratePrescriptionRequest):
    """兼容旧前端的别名"""
    return await generate(request)
