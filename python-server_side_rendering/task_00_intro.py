def generate_invitations(template, attendees):
    if not isinstance(template, str):
        print(f"Invalid input: template must be a string, got {type(template).__name__}.")
        return
    if not isinstance(attendees, list):
        print(f"Invalid input: attendees must be a list, got {type(attendees).__name__}.")
        return
    if not all(isinstance(a, dict) for a in attendees):
        print("Invalid input: attendees must be a list of dictionaries.")
        return
    if template.strip() == "":
        print("Template is empty, no output files generated.")
        return
    if not attendees:
        print("No data provided, no output files generated.")
        return

    fields = ("name", "event_title", "event_date", "event_location")
    for i, attendee in enumerate(attendees, 1):
        text = template
        for f in fields:
            v = attendee.get(f, "N/A")
            text = text.replace(f"{{{f}}}", "N/A" if v is None else str(v))
        try:
            with open(f"output_{i}.txt", "w", encoding="utf-8") as file:
                file.write(text)
        except OSError as e:
            print(f"Error writing output_{i}.txt: {e}")
