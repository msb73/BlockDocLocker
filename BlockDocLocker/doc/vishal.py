logs = ["0:start:0", "1:start:3","2:start:4", "2:end:4", "1:end:6", "0:end:10"]
def schedules(logs, n):
    stack = []
    result = [0]*n
    prev_time = 0
    prev_command = None
    for log in logs:
        logls = log.split(":")
        print(logls)
        id, command, time = int(logls[0]), logls[1], int(logls[2])
        # print(f"{prev_time=}   {time=}")
        if stack:
            if command == "start":
                result[stack[-1]] += (time - prev_time) 
                stack.append(id) 
            else:
                if prev_command == "start":
                    result[stack[-1]]+=1 
                result[stack.pop()] += (time - prev_time)
        else:
            stack.append(id)
        prev_time =  time
        prev_command = command
    return result
print(schedules(logs, 3))