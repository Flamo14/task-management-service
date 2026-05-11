# Task Creation Module

## Pattern Used
Factory Pattern

## Purpose
This module is responsible for creating Task objects in a centralized and consistent way.

The factory encapsulates:
- task id generation
- default status assignment
- task object initialization

## Why Factory Pattern
The Factory Pattern was selected because task creation contains initialization logic and default values.

Using a factory keeps object creation separate from business orchestration logic in TaskService.

This improves:
- separation of concerns
- maintainability
- modularity

## Interaction With Other Components

TaskService:
- validates business rules
- delegates task creation to TaskFactory

TaskFactory:
- creates Task instances
- applies default values

TaskRepository:
- persists created tasks

## Architecture Flow

TaskService
    ↓
TaskFactory
    ↓
TaskRepository