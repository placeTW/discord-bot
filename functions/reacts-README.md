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
      "reactions": list[str],
      "match_link_id": str (optional),
      "other_match_link_ids": list[str] (optional),
      "react_with_all": boolean (optional),
      "react_with_one": boolean (optional)
    }
  ],
  "possible_replies": [
    {
      "chance": float,
      "message": str,
      "type": str (optional)
    }
  ]
}
```

## Description of the JSON structure

`criteria`: A list of objects that define the criteria for a message to match the reaction. A message must match all of the criteria in order to trigger the reaction.
- `keywords`: A list of keywords that the message must contain. If `match_whole_word` is `true`, the message must contain the entire keyword. If `match_whole_word` is `false`, the message must contain the keyword as a substring.
- `match_whole_word`: A boolean that determines whether the keyword must be a whole word or a substring.
- `match_link_id`: An optional string that specifies the link ID of the message that the criteria should match. If specified, this is used to send a reply that has the same link ID as the matching criteria.

`possible_reactions`: The possible reactions that the bot will react to the original message to if the criteria match.
- `chance`: A float that represents the probability of the reaction occurring. This should be a value between 0 and 1.
- `reactions`: A list of strings that represent the reactions that the bot can use. These should be discord emoji names, which can be found when you type `\:emoji:` in a discord message.
- `match_link_id`: An optional string that specifies the link ID that the reaction should match. If specified, the reaction will only trigger if the criteria with the specified link ID matches.
- `other_match_link_ids`: An optional list of strings that specify link IDs of other criteria that can trigger the reaction. If specified, the reaction will trigger if any of the criteria with the specified link IDs match.
- `react_with_all`: An optional boolean that determines whether the bot should react with **all** of the specified reactions if the reaction occurs.
- `react_with_one`: An optional boolean that determines whether the bot should react with **only one** of the specified reactions if the reaction occurs.
  - If `react_with_all` and `react_with_one` are both `true`, `react_with_all` will take precedence.
  - If `react_with_all` and `react_with_one` are both `false`, the probability is calcuated per reaction.


`possible_replies`: The possible replies that the bot will reply to the original message with if the criteria match.
- `chance`: A float that represents the probability of the reply occurring. This should be a value between 0 and 1.
- `message`: A string that represents the reply message that the bot will use.
- `type`: An optional string that specifies the type of the reply message. 
  - The type can be one of the following: 
    - `text`: The bot will send the text as the reply message.
    - TODO: Multimedia types - `message` is a path to the file that the bot will send as the reply message. The file should be put in the `resources/reacts/content` directory.
      - `image`
      - `video`
      - `audio`
      - `file`
    