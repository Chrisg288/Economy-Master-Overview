# Product Tree ↔ Datagrid Linking

The Human tree and Comparator datagrid are linked through stable identifiers.

| Tree level | Record link field |
|---|---|
| Human needs root | all 10,000 records |
| Need | `need_id` |
| Fulfillment class | `fulfillment_id` |
| Product category | `category_group_id` |
| Product page | `page_id` |
| Product leaf | `record_id` / `product_node_id` |

Selecting a tree node filters the datagrid to that node. Clicking a datagrid row selects and expands the exact product node in the tree.

The product pages contain no more than 50 leaves, so the tree remains usable even though it contains 10,000 products.
