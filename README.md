### How deploy?

- `aws configure` To configure your AWS credentials in local. 
- Install AWS CDK `npm install -g aws-cdk`
- cd project.
- `cdk bootstrap`
- `cdk deploy BackendStack`
- Copy apigateway url from console
- Create the file `frontend/.env` and create a env var with name `REACT_APP_BACKEND_ENDPOINT_URL` and put this endpoint here.
- `npm install and npm run build`
- `cdk deploy FrontedStack`
- Look for the app url inside cloudfront in your AWS Account
- Test
- Ensure to execute `cdk destroy` for delete all the resources and avoid charges.