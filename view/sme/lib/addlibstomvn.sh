#!/bin/sh

mvn install:install-file -DgroupId=org.jgrapht -DartifactId=jgrapht-jdk1.6 -Dversion=0.8.3-SNAPSHOT -Dpackaging=jar -Dfile=./jgrapht-jdk1.6.jar || echo "\nFailed to install JGRAPHT\n"
