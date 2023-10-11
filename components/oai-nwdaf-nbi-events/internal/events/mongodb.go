package events

import (
	"context"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

// ------------------------------------------------------------------------------
// This method connect to mongoDB
func ConnectMongo(uri string) (*mongo.Client, context.Context, context.CancelFunc, error) {

	// ctx will be used to set deadline for process, here deadline will of 10 seconds.
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	// mongo.Connect return mongo.Client method
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(uri))
	return client, ctx, cancel, err
}

// ------------------------------------------------------------------------------
// This method closes mongoDB connection and cancel context.
func CloseMongo(client *mongo.Client, ctx context.Context, cancel context.CancelFunc) {

	// CancelFunc to cancel to context
	defer cancel()

	// client provides a method to close a mongoDB connection.
	defer func() {
		// client.Disconnect method also has deadline. returns error if any,
		if err := client.Disconnect(ctx); err != nil {
			panic(err)
		}
	}()
}

// ------------------------------------------------------------------------------
// This method used to ping the mongoDB, return error if any.
func PingMongo(client *mongo.Client, ctx context.Context) error {

	// mongo.Client has Ping to ping mongoDB, deadline of the Ping method will be determined by cxt
	if err := client.Ping(ctx, readpref.Primary()); err != nil {
		return err
	}
	return nil
}
