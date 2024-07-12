# Reacts

A core feature of the PlaceTW bot is the ability to randomly react to a message that matches a certain criteria with a corresponding related message or reaction. 

## Creating a new reaction

To create a new reaction, you need to create a new JSON file in the `resources/reacts` directory. The file should be named after the reaction you want to create (ex. `tw` for a reaction that reacts to messages relating to Taiwan). The name is used for logging the reaction in the database, so it should be short.

The JSON file should have the following structure:

```json
{
  "criteria": [
    {
      "keywords": list[str],
      "match_whole_word": boolean,
      "match_link_id": str (optional)
    }
  ],
  "possible_reactions": [
    {
      "chance": float,
      "match_link_id": str (optional),
      "other_match_link_ids": list[str] (optional),
      "reactions": list[str],
      "react_with_all": boolean (optional),
      "max_react_limit": int (optional)
    }
  ],
  "possible_replies": [
    {
      "chance": float,,
      "match_link_id": str (optional),
      "other_match_link_ids": list[str] (optional),
      "message": str,
      "type": str (optional)
    }
  ]
}
```

Refer to the comments in the code for more information on each field.
