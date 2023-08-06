# cdk-valheim

A high level CDK construct of [Valheim](https://www.valheimgame.com/) dedicated server.

## API

See [API.md](API.md)

## Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
ValheimWorld(stack, "ValheimWorld",
    cpu=2048,
    memory_limit_mi_b=4096,
    environment={
        "SERVER_NAME": "CDK Valheim",
        "WORLD_NAME": "Amazon",
        "SERVER_PASS": "fargate"
    }
)
```

## Testing

* Snapshot

```sh
yarn test
```

* Integration

```sh
npx cdk -a "npx ts-node src/integ.valheim.ts" diff
npx cdk -a "npx ts-node src/integ.valheim.ts" deploy
```
