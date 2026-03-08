package service

import model.Task
import repository.TaskRepository

class TaskService(taskRepository: TaskRepository) {

  def createTask(task: Task): Task = {
    taskRepository.create(task)
  }

  def getAllTasks: List[Task] = {
    taskRepository.getAll
  }

  def getTaskById(id: Long): Option[Task] = {
    taskRepository.getById(id)
  }

  def updateTask(id: Long, task: Task): Option[Task] = {
    taskRepository.update(id, task)
  }

  def deleteTask(id: Long): Boolean = {
    taskRepository.delete(id)
  }
}