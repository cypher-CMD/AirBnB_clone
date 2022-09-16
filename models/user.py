#!/usr/bin/python3
"""
The User Module for AirBnB Console
"""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents a User data set."""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
