package main

import (
	"os"
	"angel"
)


func main(){
	c := new(angel.AngelClient)
	c.Client_id = os.Getenv("angelist_client") 
	c.Client_secret = os.Getenv("angelist_secret")

	//You can now perform unauthenticated queries against the AngelList APi
	//To perform authenticated queries (which includes any PUT/POST/DELETE queries)
	//you need an access token

	url := c.AuthorizeUri()

	//Redirect users to url, and record the code sent in the callback

	result, err := c.RequestAccessToken(code)

	//You can now perform authenticated queries against the AngelList API
}
