1. At most 1 image(s) may be provided in one request.
```
smolagents.utils.AgentGenerationError: Error in generating model output:
litellm.BadRequestError: watsonxException - {"errors":[{"code":"invalid_input_argument","message":"Invalid input argument for Model 'meta-llama/llama-3-2-90b-vision-instruct': At most 1 image(s) may be provided in one request.","more_info":"https://cloud.ibm.com/apidocs/watsonx-ai"}],"trace":"0a6a011bb0f7050226d320447255f295","status_code":400}
(venv) shankarpentyala@macbookpro visionandbrowseragents 
```

2. At most 5 image(s) may be provided in one request
litellm.BadRequestError: watsonxException - {"errors":[{"code":"invalid_input_argument","message":"Invalid input argument for Model 'ibm/granite-vision-3-2-2b': At most 5 image(s) may be provided in one request.","more_info":"https://cloud.ibm.com/apidocs/watsonx-ai"}],"trace":"8083a25af3da8f2c177a33a11796c2a2","status_code":400}

3. litellm.BadRequestError: watsonxException - {"errors":[{"code":"invalid_input_argument","message":"Invalid input argument for Model 'meta-llama/llama-guard-3-11b-vision': At most 1 image(s) may be provided in one request.","more_info":"https://cloud.ibm.com/apidocs/watsonx-ai"}],"trace":"86a9609526226425a50e2d31bb256b41","status_code":400}

4.