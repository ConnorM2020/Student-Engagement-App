# Use Microsoft's official .NET 6 SDK image for building the app.
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build-env
WORKDIR /app

# Copy csproj and restore as distinct layers.
COPY src/stEngage.csproj ./
RUN dotnet restore

# Copy everything else from the src directory and build.
COPY src/ ./
RUN dotnet publish -c Release -o out

# Build runtime image using the official .NET 6 runtime.
FROM mcr.microsoft.com/dotnet/aspnet:6.0
WORKDIR /app
COPY --from=build-env /app/out .
EXPOSE 80

ENTRYPOINT ["dotnet", "stEngage.dll"]
