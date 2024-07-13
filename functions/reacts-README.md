# Reacts

A core feature of the PlaceTW bot is the ability to randomly react to a message that matches a certain criteria with a corresponding related message or reaction. 

## JSON template for creating a new reaction

To create a new reaction, you need to create a new JSON file in the `resources/reacts` directory. The file should be named after the reaction you want to create (ex. `tw` for a reaction that reacts to messages relating to Taiwan). The name is used for logging the reaction in the database, so it should be short.

The JSON file should have the following structure:

```json
{
  "criteria": [
    {
      "keywords": list[str],
      "match_whole_word": boolean,
      "criteria_link": str (optional)
    }
  ],
  "possible_reactions": [
    {
      "condition": str (optional),
      "chance": float,
      "reactions": list[str],
      "react_with_all": boolean (optional),
      "max_react_limit": int (optional),
    }
  ],
  "possible_replies": [
    {
      "condition": str (optional),
      "chance": float,
      "message": str,
      "type": str (optional),
      "multiplier": int (optional),
      "mention_author": boolean (optional),
    }
  ]
}
```

Refer to the comments in the code for more information on each field.
