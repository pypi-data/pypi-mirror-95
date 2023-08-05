import sys
import numpy as np
from scipy.sparse import csr_matrix

if len(sys.argv) < 2:
    import mfem.ser as mfem
elif sys.argv[1] == 'par':
    import mfem.par as mfem    


smat = csr_matrix([[1,2,3,], [0, 0, 1], [2, 0, 0]])
mmat = mfem.SparseMatrix(smat)

offset1 = mfem.intArray([0, 3, 6])
offset2 = mfem.intArray([0, 3, 6])

print('BlockOperator')
m = mfem.BlockOperator(offset1, offset2)
m.SetBlock(0, 0, mmat)
print(m._offsets[0].ToList())
print(m._offsets[1].ToList())
print(m._linked_op)

print('BlockOperator')
m = mfem.BlockOperator(offset1)
m.SetBlock(0, 1, mmat)
m.SetDiagonalBlock(1, mmat)
print(m._offsets.ToList())
print(m._linked_op)

print('BlockDiagonalPreconditioner')
m = mfem.BlockDiagonalPreconditioner(offset1)
m.SetDiagonalBlock(1, mmat)
print(m._offsets.ToList())
print(m._linked_op)

print('BlockLowerTriangularPreconditioner')
m = mfem.BlockLowerTriangularPreconditioner(offset1)
m.SetDiagonalBlock(1, mmat)
try:
   m.SetBlock(0, 1, mmat)   
except ValueError:
   print("this cause value error")
m.SetBlock(1, 0, mmat)   
print(m._offsets.ToList())
print(m._linked_op)
