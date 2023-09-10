
from gateway.api_gateway import ApiGateway
from handlers.job_handler import job_handler_init


if __name__ == '__main__':
    ApiGateway().run()
    job_handler_init()