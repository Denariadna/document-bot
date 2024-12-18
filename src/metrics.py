from prometheus_client import Counter, Histogram

BUCKETS = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0,
    1.2,
    1.4,
    1.6,
    1.8,
    2.0,
    float('+inf'),
]

LATENCY = Histogram(
    'latency_seconds',
    'Время выполнения операций',
    labelnames=['operation'],
    buckets=BUCKETS,
)

TOTAL_SEND_MESSAGES = Counter(
    'send_messages_total',
    'Количество отправленных сообщений',
    labelnames=['operation'],
)
