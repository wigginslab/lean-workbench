package main 

import (
	"os"
"log"
	angel "github.com/ChimeraCoder/goangel"
)


func main(){
	c := new(angel.AngelClient)
	c.Client_id = os.Getenv("angelist_id") 
	c.Client_secret = os.Getenv("angelist_secret")

	//You can now perform unauthenticated queries against the AngelList APi
	//To perform authenticated queries (which includes any PUT/POST/DELETE queries)
	//you need an access token

	//url := c.AuthorizeUri()

	//Redirect users to url, and record the code sent in the callback

	//result, err := c.RequestAccessToken(code)
  result, err := c.RequestAccessToken("93c9170d396838fef5b9209b1d4571c8")

	if err != nil {panic(err)}
	log.Printf("Client %v", c)
	log.Printf("Result %v", result)

	//You can now perform authenticated queries against the AngelList API
}
