/*
Copyright 2017 The Nuclio Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main

import (
	"github.com/nuclio/nuclio-sdk-go"
    "encoding/json"
    "fmt"
)

func toJson(body []byte) map[string]interface{} {
	var result map[string]interface{}
	json.Unmarshal(body, &result)
	return result
}

//https://github.com/nuclio/nuclio-sdk/blob/master/event.go
func Handler(context *nuclio.Context, event nuclio.Event) (interface{}, error) {
	context.Logger.Info("This is an unstrucured %s", "log")
    //{"index":0,"SepalLength":5.1,"SepalWidth":3.5,"PetalLength":1.4,"PetalWidth":0.2,"Species":"setosa"}
    body := event.GetBody()
    fmt.Printf("body: %s", string(body))
    j := toJson(body)
    fmt.Printf("result: %v", j)
    data := j["data"].(map[string]interface{})
    columns := j["columns"].([]interface{})

    ratio := data[columns[0].(string)].(float64) / data[columns[1].(string)].(float64)
    fmt.Println(ratio)
    resp, _ := json.Marshal(ratio)
	return nuclio.Response{
		StatusCode:  200,
		ContentType: "application/text",
		Body:       resp,
	}, nil
}
