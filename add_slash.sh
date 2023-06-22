#!/bin/bash

input_file="input.txt"
output_file="output.txt"

# 检查输入文件是否存在
if [ ! -f "$input_file" ]; then
    echo "输入文件 $input_file 不存在"
    exit 1
fi

# 清空输出文件
> "$output_file"

# 逐行读取输入文件并添加斜杠
while IFS= read -r line; do
    modified_line="/$line"
    echo "$modified_line" >> "$output_file"
done < "$input_file"

echo "处理完成，结果已保存至 $output_file"
