import httpcore

pool = httpcore.ConnectionPool()

for j in range(10):
    pool._pool.append(
        httpcore.HTTPConnection(httpcore.Origin(b"https", b"www.google.com", 443))
    )

response = pool.request(
    "GET", "https://www.google.com", extensions={"timeout": {"pool": 5}}
)  # timeout error
