#!/bin/bash
# Script to run the server

# Set environment variable
export NODE_ENV=development

# Run the server using node directly
node --loader tsx server/index.ts
