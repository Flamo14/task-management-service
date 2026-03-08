package routes

import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import spray.json.DefaultJsonProtocol._
import model.Task
import service.TaskService

class TaskRoutes(taskService: TaskService) {

  val routes =
    pathPrefix("tasks") {
      pathEnd {
        get {
          complete(taskService.getAllTasks)
        } ~
        post {
          entity(as[Task]) { task =>
            complete(taskService.createTask(task))
          }
        }
      } ~
      path(LongNumber) { id =>
        get {
          taskService.getTaskById(id) match {
            case Some(task) => complete(task)
            case None => complete(404, "Task not found")
          }
        } ~
        put {
          entity(as[Task]) { task =>
            taskService.updateTask(id, task) match {
              case Some(updatedTask) => complete(updatedTask)
              case None => complete(404, "Task not found")
            }
          }
        } ~
        delete {
          if (taskService.deleteTask(id)) {
            complete(204, "")
          } else {
            complete(404, "Task not found")
          }
        }
      }
    }
}