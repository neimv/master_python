
from nodes import Node


head = None

for count in range(1, 6):
    head = Node(count, head)

# Validando

while head is not None:
    print(head.data)
    head = head.next

probe = head

while probe is not None:
    print(probe.data)
    probe = probe.next

probe = head
target_item = 2

while probe is not None and target_item != probe.data:
    probe = probe.next

if probe != None:
    print(f"Target item {target_item} has been found")
else:
    print(f"target item {target_item} is not in the link listed")



