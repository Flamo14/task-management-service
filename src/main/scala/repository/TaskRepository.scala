package repository

import model.Task
import scala.collection.mutable

class TaskRepository {
  private val tasks = mutable.Map[Long, Task]()
  private var idCounter = 0L

  def create(task: Task): Task = {
    idCounter += 1
    val newTask = task.copy(id = idCounter)
    tasks(idCounter) = newTask
    newTask
  }

  def getAll: List[Task] = tasks.values.toList

  def getById(id: Long): Option[Task] = tasks.get(id)

  def update(id: Long, updatedTask: Task): Option[Task] = {
    tasks.get(id).map { _ =>
      val taskToUpdate = updatedTask.copy(id = id)
      tasks(id) = taskToUpdate
      taskToUpdate
    }
  }

  def delete(id: Long): Boolean = {
    tasks.remove(id).isDefined
  }
}