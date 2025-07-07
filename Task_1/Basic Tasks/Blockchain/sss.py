import random

PRIME = 208351617316091241234326746312124448251235562226470491514186331217050270460481

def make_polynomial(secret, k):
    return [secret] + [random.randrange(0, PRIME) for i in range(k - 1)]

def evaluate_polynomial(poly, x):
    j=sum=0
    for i in poly:
        t=(pow(x,j, PRIME)*i)% PRIME
        j+=1
        sum+=t
    return sum % PRIME

def generate_shares(secret, n, k):
    poly = make_polynomial(secret, k)
    shares = [(x, evaluate_polynomial(poly, x)) for x in range(1, n + 1)]
    return shares

def lagrange_interpolation(x, x_s, y_s):
    total = 0
    k = len(x_s)
    for i in range(k):
        xi, yi = x_s[i], y_s[i]
        prod = yi
        for j in range(k):
            if i != j:
                xj = x_s[j]
                # Compute the modular inverse
                inv = pow(xi - xj, -1, PRIME)
                prod *= (x - xj) * inv
                prod %= PRIME
        total += prod
        total %= PRIME
    return total

# Example usage

secret =int(input("enter message: "))
n = 5   # total shares
k = 3   # threshold to reconstruct
shares = generate_shares(secret, n, k)
 
print("Generated Shares:")
for share in shares:
    print(share)
sample = random.sample(shares, k)
print("reconstructing secret using shares:")
for i in sample:
    print((i))
x_s, y_s = zip(*sample)
recovered_secret = lagrange_interpolation(0, x_s, y_s)
    
print("\nReconstructed Secret:", recovered_secret)
