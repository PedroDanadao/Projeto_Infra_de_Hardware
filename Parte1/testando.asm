.data
	number1: $0
	j start

.text
	add $0, $0, $0
	and $0, $0, $0
	slt $t0, $a0, $a0
	xor $a1, $a0, $a3
	sll $3, $7, 4
	or $t5, $t6, $a0
	jr $31
	mflo $5
	mfhi $31
#	sw $1, 3276($2)
	lb $31, -4300($31)
	lw $1, -100($2)
	sll $1, $2, 31
	addi $3, $7, -17300
	addiu $5, $7, -17632
	ori $5, $8, 179
	xori $13, $19, 132
	slti $6, $29, 1000
	lui $3, 65535
	lw $1, -100($2)
	div $1, $2, 100
	syscall
