package model

import spray.json.DefaultJsonProtocol._

case class Task(id: Long, title: String, description: Option[String], status: String)

object Task {
  implicit val taskFormat = jsonFormat4(Task.apply)
}