import model.Task
import java.time.LocalDate
object Main extends App {

val task = Task(
    id = 1,
    title = "Learn Scala",
    description = "Study the basics of Scala programming language.",
    status = "Pending",
    priority = "Medium",
    startDate = LocalDate.parse("2023-10-01"),
    endDate = LocalDate.parse("2023-10-31")
)
}