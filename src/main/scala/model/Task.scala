package model
import java.time.LocalDate

case class Task(
    id: Long,
    title: String,
    description: String,
    status: String = "Pending",
    priority: String = "Medium",
    startDate: java.time.LocalDate,
    endDate: java.time.LocalDate
)
