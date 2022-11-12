from math import sqrt

RQ3_FILE = r'rq3_data_by_class.csv'

# writer.write('Class,TotalTestabilitySmells,TestabilitySmellsDensity,TotalTests,TestDensity\n')
def _compute():
    a = b = c = d= 0
    with open(RQ3_FILE, 'r') as file:
        is_header = True
        for line in file:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 4:
                if int(tokens[1]) > 0:
                    if int(tokens[3]) > 0:
                        d += 1
                    else:
                        b += 1
                else:
                    if int(tokens[3]) > 0:
                        c += 1
                    else:
                        a += 1
    # compute phi-coefficient
    phi = (a*d - c*b)/sqrt((a+b)*(c+d)*(a+c)*(b+d))
    print('phi coefficient: ' + str(phi))


if __name__ == "__main__":
    _compute()