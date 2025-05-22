
import os
import sys
import asyncio
from datetime import datetime

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from dotenv import load_dotenv
from dataclasses import dataclass

import snowflake.connector
import pymongo

from mcp.server.fastmcp import FastMCP, Context

load_dotenv(override=True)


# Defining Schema for MongoDb Memory Management
session_data = {
    "session_id": f"session_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
    "user": None,
    "start_time": datetime.now(),
    "end_time": None,
    "queries_executed": 0,
    "queries": []
}

@dataclass
class AppContext:
    snowflake_conn: snowflake.connector.SnowflakeConnection
    mongodb_conn : pymongo.MongoClient

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    
    print('Snowflake Connection Success', file=sys.stderr)
    # Initialize Snowflake Connector Object on startup
    snowflake_conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["snowflake_mcp"]
    collection = db["sessions_data"]

    session_data["user"] = os.getenv('SNOWFLAKE_USER')



    try:
        yield AppContext(snowflake_conn=snowflake_conn,mongodb_conn=client)
        print('Context Passing Success', file=sys.stderr)
        
    finally:
        # Close the Snowflake Connection on shutdown
        snowflake_conn.close()
        long_term_memory(collection)
        print('Snowflake Disconnected', file=sys.stderr)


# Memory Management
def long_term_memory(mongodb_collection):
    mongodb_collection.insert_one(session_data)
    print("Session Stored in MongoDB",file=sys.stderr)


# Create an MCP server object from FastMCP
mcp = FastMCP(
    name="snowflake admin mcp",
    instructions="MCP Server for Snowflake Data Warehouse Connection & Admin Use Cases",
    lifespan=app_lifespan,
    )


# Tools
@mcp.tool()
def run_snowflake_query(ctx: Context, query: str) -> str:
    """
    Execute a SQL query against the Snowflake database.

    Args:
        ctx: The MCP server provided context containing the Snowflake connection.
        query: A valid SQL query string to execute.
    """
    try:
        conn = ctx.request_context.lifespan_context.snowflake_conn
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        session_data["queries"].append(query)
        session_data["queries_executed"] += 1
        return str(result)
        
    except Exception as e:
        return f"Error executing query: {str(e)}"
    

if __name__ == "__main__":
    mcp.run()
