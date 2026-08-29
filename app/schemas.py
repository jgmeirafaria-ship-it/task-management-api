from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    """Dados que o cliente envia para criar uma tarefa nova."""
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """Dados que o cliente pode enviar para atualizar uma tarefa."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Dados que a API devolve ao cliente, representando uma tarefa."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None