
# how many transfills of an empty al80 from a full HP119 until the 80 is full?
# formulas below probably can be simplified significantly, but is accurate

# acutal capacity in cu ft
CAP_80 = 77.4
CAP_119 = 119.0
# starting psi of each cylinder
p_80 = 0.0
p_119 = 3400.0
# rated psi of each cylinder
r_80 = 3000.0
r_119 = 3442.0

equiv_cap = r_80 * CAP_119 / r_119
print("capacity of 119 at {:.0f}psi is: {:.1f}".format(r_80, equiv_cap))
total_cap = equiv_cap + CAP_80
print("capacity of 119 and 80 at {:.0f}psi is: {:.1f}\n".format(r_80, total_cap))

def single_transfill(p80, p119):
    starting_cuft = CAP_119*(p119/r_119) + CAP_80*(p80/r_80)
    print("starting cuft: {:.0f}".format(starting_cuft))

    ending_psi = r_80 * starting_cuft / total_cap
    print("ending psi: {:.0f}".format(ending_psi))
    return ending_psi

count = 0
while (p_80 < 3000):
    count+=1
    p_80 = single_transfill(p_80, p_119)

print("took {} transfills to fill tank".format(count))
