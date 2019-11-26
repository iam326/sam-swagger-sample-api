# sam-swagger-sample-api

SAM ＋ Swagger で API を作成するサンプル。

## Dependency

```
$ python --version
Python 3.7.5

$ pip --version
pip 19.2.3 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)

$ sam --version
SAM CLI, version 0.22.0
```

## Setup

```
$ pip install pip==19.2.3 aws-sam-cli==0.22.0

$ aws s3 mb s3://iam326.sam-swagger-sample
```

## Usage

```
./deploy.sh
```

## Memo

- 雛形作成

```
$ sam init --runtime python3.7 --name sam-swagger-sample-api
```

- Swagger Editor の起動

```
$ docker pull swaggerapi/swagger-editor
$ docker run -d -p 80:8080 swaggerapi/swagger-editor
http://localhost/
```

- Lambda の Runtime で指定した Python のバージョンと、ローカルのバージョンを合わせる必要がある

- 記載した pip や sam 以外のバージョンを使用すると、`sam build`でエラーが発生する可能性がある
