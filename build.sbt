name := "task-management-service"

version := "1.0"

scalaVersion := "3.3.3"

libraryDependencies ++= Seq(
  "org.http4s" %% "http4s-ember-server" % "0.23.26",
  "org.http4s" %% "http4s-dsl" % "0.23.26",
  "org.http4s" %% "http4s-circe" % "0.23.26",
  "io.circe" %% "circe-generic" % "0.14.7",
  "io.circe" %% "circe-parser" % "0.14.7"
)