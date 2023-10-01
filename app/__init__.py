from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from starlette.authentication import AuthenticationError
from starlette.middleware import Middleware

from app.api import api_router
from setting import setting
from .fastapi.middlewares import AuthenticationMiddleware, AuthBackend, ResponseLogMiddleware
from .helper.exception_handler import fastapi_error_handler, request_validation_exception_handler, \
    validation_exception_handler, http_exception_handler, CommonException, base_exception_handler
from .helper.db import db_engine
from starlette_context.middleware import ContextMiddleware
from starlette.requests import Request, HTTPConnection

from .helper.prometheus_middleware import PrometheusMiddleware, handle_metrics
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased


class GetLanguageMiddleware(ContextMiddleware):
    async def set_context(self, request: Request) -> dict:
        return {"lang": request.headers.get('Accept-Language')}


def on_auth_error(conn: HTTPConnection, exc: AuthenticationError):
    raise HTTPException(status_code=401, detail="Unauthorized")


middleware = [
    Middleware(
        GetLanguageMiddleware,
    ),
    Middleware(
        AuthenticationMiddleware,
        backend=AuthBackend(),
        on_error=on_auth_error,
    ),
    Middleware(ResponseLogMiddleware),
]


def create_app() -> FastAPI:
    app = FastAPI(
        title=setting.PROJECT_TITLE, docs_url='/core/docs',
        middleware=middleware
    )

    app.add_middleware(PrometheusMiddleware, app_name="edusun-service",
                       exclude_paths=['/api/v1/health/check', '/metrics'])
    app.add_route("/metrics", handle_metrics)
    app.include_router(api_router, prefix="/api")
    if setting.JAEGER_ENABLED:
        sampler = TraceIdRatioBased(setting.JAEGER_SAMPLING_RATE)
        trace.set_tracer_provider(
            TracerProvider(
                resource=Resource.create({SERVICE_NAME: "EduSun Service"}),
                sampler=sampler
            )
        )
        jaeger_exporter = JaegerExporter(
            agent_host_name=setting.JAEGER_AGENT_HOST, agent_port=setting.JAEGER_AGENT_PORT,
        )
        span_processor = BatchSpanProcessor(jaeger_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
        SQLAlchemyInstrumentor().instrument(engine=db_engine)
        RequestsInstrumentor().instrument()
        FastAPIInstrumentor.instrument_app(app, excluded_urls='health/*,metrics')

    # Set all CORS enabled origins
    # if setting.BACKEND_CORS_ORIGINS:
    #     app.add_middleware(
    #         CORSMiddleware,
    #         allow_origins=[str(origin) for origin in setting.BACKEND_CORS_ORIGINS],
    #         allow_credentials=True,
    #         allow_methods=["*"],
    #         allow_headers=["*"],
    #     )

    # Add exception
    app.add_exception_handler(CommonException, base_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, fastapi_error_handler)

    return app
