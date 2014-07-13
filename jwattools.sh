#!/bin/sh
java -Xms256m -Xmx1048m -XX:PermSize=64M -XX:MaxPermSize=256M -jar target/jwat-tools-*-jar-with-dependencies.jar $@
