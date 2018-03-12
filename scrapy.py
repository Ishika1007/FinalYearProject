
def nextPermutation(nums):
    flag = False
    for i in range(len(nums) - 1, 0, -1):
        if nums[i] > nums[i - 1] and i == len(nums) - 1:
            temp = nums[i]
            nums[i] = nums[i - 1]
            nums[i - 1] = temp
            flag = True
            print("here")
            break
        elif nums[i] > nums[i - 1]:
            mini = nums[i]
            index = i
            for j in range(i, len(nums)):
                if nums[j] > nums[i - 1]:
                    mini = min(nums[j], mini)
                    index = j
                else:
                        break
            temp = nums[index]
            nums[index] = nums[i - 1]
            nums[i - 1] = temp
            flag = True
            nums = nums[:i] + sorted(nums[i:])
            print(nums)
            break
        else:
            continue

        if flag == True:
            break
    if flag == False:
        nums = sorted(nums)

def main():

    # parse xml file
     nextPermutation([1,3,2])
if __name__ == "__main__":
    # calling main function
    main()