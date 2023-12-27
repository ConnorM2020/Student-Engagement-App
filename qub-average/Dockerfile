FROM golang:1.18 as builder

WORKDIR /app

COPY src/ .

ENV GO111MODULE=off

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:latest

RUN apk --no-cache add ca-certificates
COPY --from=builder /app/app /app

EXPOSE 80
CMD ["/app"]