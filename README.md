# Google Cloud Platform Cookbook
This is the code repository for [Google Cloud Platform Cookbook](https://www.packtpub.com/virtualization-and-cloud/google-cloud-platform-cookbook?utm_source=github&utm_medium=repository&utm_campaign=9781788291996), published by [Packt](https://www.packtpub.com/?utm_source=github). It contains all the supporting project files necessary to work through the book from start to finish.
## About the Book
Google Cloud Platform is a cloud computing platform that offers products and services to host applications using a state-of-the art infrastructure and technology. You can build and host applications and websites, store data, and analyze data on Google's scalable infrastructure. This book follows a recipe-based approach, giving you hands-on experience to make the most out of Google Cloud services.

This book starts with practical recipes, giving you heads-up on how to utilize Google Cloud's common services. Then, you’ll see how to make full use of Google Cloud components such as Networking, Security, Management, and Developer tools. Next, we deep dive into implementing core Google Cloud services into your organization, with practical recipes on App Engine, Compute Engine Microservices with Cloud functions, Virtual Networks, and Cloud Storage. Later, we provide recipes on implementing authentication and security, Cloud APIs, command-line management, deployment management, and Cloud SDK.

Finally, we cover administration troubleshooting tasks with compute and container engine and how to monitor your organization’s efficiency with best practices. By the end of this book, you’ll have a complete understanding of how to implement Google Cloud services in your organization with ease.
## Instructions and Navigation
All of the code is organized into folders. For example, Chapter02.

Install the Google Cloud SDK: https://cloud.google.com/sdk/docs/

For testing Python code, install the Google Cloud Client Library for Python:

pip install google-cloud

Or: https://googlecloudplatform.github.io/google-cloud-python/

For testing NodeJS code, you can do an npm install of the required Node.js packages:

https://cloud.google.com/nodejs/docs/reference/libraries

The code will look like the following:
```
#! /bin/bash
apt-get update
apt-get install -y apache2
cat <<EOF > /var/www/html/index.html
<html><body><h1>Hello World</h1>
<p>Web server on the alpha and beta networks</p>
</body></html>
EOF
```

The readers should have a Linux VM, which is where the examples can be downloaded to and executed. The Linux VM will act as your development machine. Make sure that your development machine has enough space to handle the number of dependencies that will be installed along with the code. A basic understanding of cloud services and GCP is necessary.

Few recipes have simple configuration of services and others will require changes to source code. Hence, a familiarity with a programming language (Python/Node.js) and basic Linux knowledge will be beneficial.

Due to the rapid evolution of tools and dependencies, there is the possibility of commands and code breaking. Head over to the documentation if you need to modify the commands/code to suit your needs.

## Related Products
* [Cloud Analytics with Google Cloud Platform](https://www.packtpub.com/big-data-and-business-intelligence/cloud-analytics-google-cloud-platform?utm_source=github&utm_medium=repository&utm_campaign=9781788839686)

* [Kubernetes for Serverless Applications](https://www.packtpub.com/networking-and-servers/kubernetes-serverless-applications?utm_source=github&utm_medium=repository&utm_campaign=9781788620376)

* [Google Cloud Platform (GCP) - For Techs [Video]](https://www.packtpub.com/application-development/google-cloud-platform-gcp-techs-video?utm_source=github&utm_medium=repository&utm_campaign=9781789137668)
