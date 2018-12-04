def request(flow):
    flow.response.content = flow.response.content.replace("application/php","image/jpeg").replace("application/x-php", "image/jpeg")
