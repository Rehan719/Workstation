import json
import os
import datetime
import asyncio
from typing import List, Dict, Any
from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.ueg.logger import VSBUEGLogger

class SATsScheduleGenerator:
    """
    Generates a 14-day intensive revision schedule for the child.
    """
    def __init__(self, output_dir: str = "outputs/education/sats_2026/revision_schedule"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.ueg = VSBUEGLogger()

    @constitutional_guard
    async def generate_schedule(self) -> Dict[str, Any]:
        """Generates a personalized 14-day schedule for Ayaan."""
        start_date = datetime.date(2026, 5, 1)
        schedule = []

        # SATs Timetable 2026
        exam_timetable = {
            11: "EXAM: English GPS",
            12: "EXAM: English Reading",
            13: "EXAM: Maths Arithmetic & Reasoning 1",
            14: "EXAM: Maths Reasoning 2"
        }

        weaknesses = [
            "Maths: Algebra & Equations",
            "Reading: 3-mark LINK structure",
            "Maths: Fractions (Mixed/Improper)",
            "English: Possessive Apostrophes"
        ]

        motivational_quotes = [
            "Keep going, Ayaan – you’ve got this!",
            "Well done, Ayaan! You’re making great progress.",
            "Great work! Arsenal would be proud of this effort.",
            "You're building your knowledge like a Minecraft pro!",
            "Every session brings you closer to your goal, Ayaan.",
            "Stay focused – you're doing amazing!",
            "Nearly there! One final push."
        ]

        for i in range(14):
            current_date = start_date + datetime.timedelta(days=i)
            day_of_month = current_date.day
            day_schedule = {
                "day": i + 1,
                "date": current_date.isoformat(),
                "sessions": [],
                "motivation": motivational_quotes[i % len(motivational_quotes)]
            }

            if day_of_month in exam_timetable:
                day_schedule["sessions"] = [
                    {"time": "09:00 - 11:00", "activity": f"SATs {exam_timetable[day_of_month]}", "goal": "Perform best", "engine": "Iman (Sulphur)"},
                    {"time": "13:00 - 14:00", "activity": "Rest & Recover: Arsenal/Minecraft time", "goal": "Recharge", "engine": "Hoshiyari (Oxygen)"},
                    {"time": "16:00 - 16:30", "activity": "Light Review for tomorrow's paper", "goal": "Confidence", "engine": "Samajh (Nitrogen)"}
                ]
                day_schedule["status"] = "SATs EXAM WEEK"
            elif i < 10: # Revision phase
                day_schedule["sessions"] = [
                    {"time": "09:00 - 09:30", "activity": f"Topic Focus: {weaknesses[i % 4]}", "goal": "Bridge gaps", "engine": "Inkashaf (Water)"},
                    {"time": "11:00 - 11:30", "activity": "Sensory Break / Physical Activity", "goal": "Prevent fatigue", "engine": "Hoshiyari (Oxygen)"},
                    {"time": "16:00 - 16:30", "activity": "Practice Paper Set & Model Answer Review", "goal": "Consistency", "engine": "Aqal (Carbon)"}
                ]
                day_schedule["status"] = "Intensive Revision"
            else: # Final Weekend prep
                day_schedule["sessions"] = [
                    {"time": "10:00 - 10:30", "activity": "Quick-fire Arithmetic & Reading inference", "goal": "Sharpness", "engine": "Soch (Phosphorus)"},
                    {"time": "14:00 - 14:30", "activity": "Mindfulness / Space Documentary", "goal": "Balance", "engine": "Hoshiyari (Oxygen)"}
                ]
                day_schedule["status"] = "Final Prep & Wellbeing"

            schedule.append(day_schedule)

        return {"revision_plan": schedule}

    async def save_markdown(self, schedule_data: Dict[str, Any]):
        md_content = "# 📅 SATs 2026: 14-Day Revision Schedule\n\n"
        md_content += "## Personalized for: Ayaan (Norbury School, Harrow)\n\n"

        for day in schedule_data["revision_plan"]:
            md_content += f"### Day {day['day']} - {day['date']} ({day['status']})\n"
            md_content += f"*{day['motivation']}*\n\n"
            for session in day["sessions"]:
                md_content += f"- **{session['time']}**: {session['activity']} (Goal: {session['goal']})\n"
            md_content += "\n---\n"

        path = os.path.join(self.output_dir, "schedule.md")
        with open(path, "w") as f:
            f.write(md_content)

        # Also save JSON
        json_path = os.path.join(self.output_dir, "schedule.json")
        with open(json_path, "w") as f:
            json.dump(schedule_data, f, indent=4)

        return path

async def main():
    gen = SATsScheduleGenerator()
    data = await gen.generate_schedule()
    await gen.save_markdown(data)
    print("Schedule generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
