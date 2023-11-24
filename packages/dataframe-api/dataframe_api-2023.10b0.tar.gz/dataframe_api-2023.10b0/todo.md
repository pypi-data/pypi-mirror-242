- column_from_1d_array doesn't need dtype argument
- namespace.column_from_1d_array(array, dtype=namespace.Float64(), name='preds') seems to break typing
- shouldn't need dtype in the above anyway?

prs to open:
- drop_nulls
- ping on shift
- top-level-functions (sigh...not looking forward to opening this one)


---

would be nice to have
- just `-> Scalar`
- be able to use Python scalars and Scalar interchangeably

little break, then:
- merge pr
- add scalar_namespace
