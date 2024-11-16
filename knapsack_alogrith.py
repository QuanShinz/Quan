
class Package:
    
    def __init__(self, location, weight, distance):
        self.package_code = None
        self.location = location
        self.weight = weight
        self.distance = distance

def ks_algorithm(packages, maximum_weight):
    n = len(packages)
    
    dp = [[0 for _ in range(maximum_weight + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(maximum_weight + 1):
            dp[i][w] = dp[i - 1][w] 
            if packages[i - 1].weight <= w:
                package_satisfied = dp[i - 1][w - packages[i - 1].weight] + packages[i - 1].weight
                if package_satisfied > dp[i][w]:
                    dp[i][w] = package_satisfied

    chosen_packages = []
    w = maximum_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen_packages.append(packages[i - 1])
            w -= packages[i - 1].weight

    unchosen_packages = [package for package in packages if package not in chosen_packages]

    return chosen_packages, unchosen_packages

def generate_invoice(packages, base_rate=10, distance_rate=0.05):
    invoice_list = []
    for package in packages:
        cost = base_rate * package.weight + distance_rate * package.distance
        invoice_list.append({"package_code": package.package_code, "cost": cost, "location": package.location})
    return invoice_list


def allocate_trucks(packages, maximum_weight):
    trucks = []
    while packages:
        truck_packages, packages = ks_algorithm(packages, maximum_weight)
        truck_packages.sort(key=lambda p: p.distance, reverse=True)  

        trucks.append(truck_packages)
    return trucks


packages_detail = [
    Package("Da Nang", 10, 750),
    Package("HCMC", 5, 1600),
    Package("Nha Trang", 7, 1000),
    Package("Dalat", 12, 1350),
    Package("Hai Phong", 4, 120)
]

packages = []
HCM_counter = 1
DAN_counter = 1
NAT_counter = 1
DL_counter = 1
HP_counter = 1
for package in packages_detail:
    if package.location == "HCMC":
        package.package_code = f"HCMC{str(HCM_counter).zfill(3)}" 
        HCM_counter += 1
    if package.location == "Da Nang":
        package.package_code = f"DAN{str(DAN_counter).zfill(3)}"  
        DAN_counter += 1
    if package.location == "Nha Trang":
        package.package_code = f"NAT{str(NAT_counter).zfill(3)}"  
        NAT_counter += 1
    if package.location == "Dalat":
        package.package_code = f"DL{str(DL_counter).zfill(3)}"  
        DL_counter += 1
    if package.location == "Hai Phong":
        package.package_code = f"HP{str(HP_counter).zfill(3)}"  
        HP_counter += 1
    packages.append(package)

maximum_weight = 25

trucks = allocate_trucks(packages, maximum_weight)

truck_number = 1
for truck in trucks:
    print(f"\nTruck {truck_number} Packages (Furthest Distance Loaded First):")
    for package in truck:
        print(f"Package Code: {package.package_code}, Location: {package.location}, Weight: {package.weight}, Distance: {package.distance}")
    
    invoices = generate_invoice(truck)
    print(f"\nTruck {truck_number} Invoices:")
    for invoice in invoices:
        print(f"Hello customer, Your Package Code: {invoice['package_code']}, Collected in Hanoi, Delivery to {invoice['location']} Cost: {invoice['cost']}")
    
    truck_number += 1


