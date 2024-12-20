

class Answers():
    def AnswerRection(place, numbers):
        msg = ""
        for x in range(len(place)):
            if place[x] != 0:
                msg = msg + f"🔴 {numbers[x]} место - занято {place[x]}\n"
            else:
                msg = msg + f"🟢 {numbers[x]} место\n"
        return msg