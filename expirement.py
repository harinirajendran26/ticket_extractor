from ticket_analysis import analyze

a = analyze("My order status has been stuck on 'processing' for six days.")
b = analyze("My order status has been stuck on 'processing' for six days without any update.")
print("without the phrase:", a.contacted_support_before)
print("with the phrase:   ", b.contacted_support_before)