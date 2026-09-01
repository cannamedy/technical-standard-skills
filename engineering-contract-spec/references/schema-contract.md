# Schema Contract Review

For each object:

| Dimension | Questions |
|---|---|
| Identity | How is this object uniquely identified? |
| Version | What schema/namespace version applies? |
| Required fields | Which fields are mandatory? |
| Optional fields | Which are optional? |
| Types | Exact scalar/object/array/enums? |
| Units | Are physical units explicit? |
| Frames | Are spatial frames explicit? |
| Time | Timestamp/revision/sequence? |
| Authority | Who may assert/update it? |
| Mutability | Read-only/read-write/derived? |
| Lifecycle | Created/updated/expired/deleted when? |
| Errors | What invalid forms are rejected? |
| Extension | How can domains extend it? |
| Compatibility | How are older/newer versions handled? |

A conceptual example is not a schema.
A schema is not complete if an implementer still has to guess semantic meaning.
