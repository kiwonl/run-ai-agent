# Weather MCP Server

This is a simple MCP server that provides weather information.

## Features

- Get the weather for a specific city.
- Get the weather for a date range.

## How to use

Send a request to the `get_weather` tool with a query string in Korean format.

- `query`: A string containing the city and date(s) in Korean format.

### Example

To get the weather for Seoul on September 3, 2025, you would call the tool with:

```
get_weather(query="서울, 25년 9월 3일")
```

To get the weather for Seoul from September 30 to October 5, 2025, you would call the tool with:

```
get_weather(query="서울, 25년 9월 30일 ~ 25년 10월 5일")
```