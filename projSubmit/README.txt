11-611 Natural Language Processing Final Project
Team Knock Knock Who's There README
Jing Wang, Tony Wang, Wei Wang

In order to run our system, please use the following steps:

1. Enter into the Graphene folder 
2. Inside the Graphene folder run: docker-compose up
3. Wait for the container to finish loading. The last message will look like the following:

############################
graphene_1     |     "relation-extraction" : {
graphene_1     |         "exploit-contexts" : false,
graphene_1     |         "exploit-core" : true,
graphene_1     |         "relation-extractor" : "org.lambda3.graphene.core.relation_extraction.impl.HeadRelationExtractor",
graphene_1     |         "separate-attributions" : false,
graphene_1     |         "separate-noun-based" : true,
graphene_1     |         "separate-purposes" : false
graphene_1     |     },
graphene_1     |     "server" : {
graphene_1     |         "host-name" : "localhost",
graphene_1     |         "path" : "",
graphene_1     |         "port" : 8080
graphene_1     |     },
graphene_1     |     "version" : {
graphene_1     |         "build-number" : "70d48441414f7e9e6a2f2527532bcdbfa1069d9d",
graphene_1     |         "name" : "Graphene-Core",
graphene_1     |         "version" : "3.0.0-SNAPSHOT"
graphene_1     |     }
graphene_1     | }
graphene_1     |  
############################

3. Access the project folder file (~/projSubmit/)
4. Run the regular commands ./answer and ./ask (answer will take several minutes, closer to 10 minutes)