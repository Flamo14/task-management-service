import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import scala.concurrent.ExecutionContextExecutor
import repository.TaskRepository
import service.TaskService
import routes.TaskRoutes

object Main extends App {
  implicit val system: ActorSystem = ActorSystem("task-management-service")
  implicit val executionContext: ExecutionContextExecutor = system.dispatcher

  val taskRepository = new TaskRepository()
  val taskService = new TaskService(taskRepository)
  val taskRoutes = new TaskRoutes(taskService)

  val bindingFuture = Http().newServerAt("localhost", 8080).bind(taskRoutes.routes)

  println(s"Server online at http://localhost:8080/")
}