# Frozen Source Integrity

This is a conditional gate. Apply it only when an authoritative source declares a freeze commit,
freeze tag, checksum, SHA-256, immutable revision, or equivalent baseline.

Before planning affected requirements:

1. identify the source and its declared baseline;
2. inspect the current revision or bytes;
3. verify the declaration using the project's stated method;
4. record the result and evidence in the Plan or traceability artifact.

If the declaration exists and verification fails, stop affected planning. Do not repair the frozen
source, treat the current checkout as authority, or continue because the content appears similar.

If no freeze metadata is declared, do not invent a repository-wide checksum or tag requirement.
