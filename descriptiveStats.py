import pandas as pd
from diagramMaker import histogramer, box_plotter
from scipy import stats

def load_and_modify_age():
    # 1- Cargar dataframe
    titanik_dataframe = pd.read_csv("titanik.csv")
    
    # 2- Corregir edades vacías, por genero, con la media de edad
    men_mean_age = titanik_dataframe.loc[titanik_dataframe.gender == "male"].age.mean()
    print("La edad promedio de los hombres es:")
    print(men_mean_age)
    women_mean_age = titanik_dataframe.loc[titanik_dataframe.gender == "female"].age.mean()
    print("La edad promedio de las mujeres es:")
    print(women_mean_age)
    print()
    titanik_dataframe.loc[
        (titanik_dataframe["gender"] == "male") & (titanik_dataframe["age"].isna()), "age"
    ] = men_mean_age
    titanik_dataframe.loc[
        (titanik_dataframe["gender"] == "female") & (titanik_dataframe["age"].isna()),
        "age",
    ] = women_mean_age
    return titanik_dataframe

titanik_dataframe = load_and_modify_age()
# 3- Calcular media, moda, rango, varianza y desviación estandar
mean_age = titanik_dataframe.age.mean()
mode_age = titanik_dataframe.age.mode()[0]
range_age = (float(titanik_dataframe.age.min()), float(titanik_dataframe.age.max()))
variance_age = 0.0
ages = titanik_dataframe.age.tolist()
ages.sort()
n_ages = len(ages)
if n_ages % 2 == 0:
    median_age = (ages[n_ages // 2] + ages[(n_ages // 2) - 1]) / 2
else:
    median_age = ages[n_ages // 2]

for age in ages:
    variance_age += (age - mean_age) ** 2
number_of_rows = titanik_dataframe.shape[0]
variance_age = variance_age / number_of_rows
standard_d_age = variance_age ** (1 / 2)


# 4- Tasa de supervivencia general
print("Tasa de supervivencia general: ")
superv_rate = titanik_dataframe.survived.mean()
print(superv_rate)
# 5- Por género
superv_rate_male = titanik_dataframe.loc[
    titanik_dataframe["gender"] == "male", "survived"
].mean()
superv_rate_female = titanik_dataframe.loc[
    titanik_dataframe["gender"] == "female", "survived"
].mean()
print("Tasa de supervivencia por genero: ")
print(f"Hombres: {superv_rate_male}")
print(f"Mujeres: {superv_rate_female}")
# 6. Realizar un histograma de las edades de los pasajeros por clase (primera, segunda y tercera).
# Proponga un modelo para la distribuci´on de la variable edad en el barco.

third_class_ages = titanik_dataframe.loc[titanik_dataframe["p_class"] == 3].age.tolist()
second_class_ages = titanik_dataframe.loc[
    titanik_dataframe["p_class"] == 2
].age.tolist()
first_class_ages = titanik_dataframe.loc[titanik_dataframe["p_class"] == 1].age.tolist()
class_age_distributions = [third_class_ages, second_class_ages, first_class_ages]

histogramer(
    "Distribución de edades",
    class_age_distributions,
    ["tercera clase", "segunda clase", "primera clase"],
)
# 7. Realizar un diagrama de cajas para las edades de los supervivientes, y otro para las edades de los
# no supervivientes. ¿Es posible extraer alguna conclusi´on?
survived_ages = titanik_dataframe.loc[titanik_dataframe["survived"] == 1].age.tolist()
not_survived_ages = titanik_dataframe.loc[
    titanik_dataframe["survived"] == 0
].age.tolist()

survive_age_distributions = [survived_ages, not_survived_ages]

box_plotter(
    "Distribución de edades", survive_age_distributions, ["sobrevivió", "no sobrevivió"]
)


# Guardo toda la data en un txt
def print_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


to_print = (
    f"Media edad: {mean_age}\nModa edad: {mode_age}\nMediana: {median_age}\nRango de edad: {range_age}"
    + f"\nVarianza de edad: {variance_age}\nDesviación estandar: {standard_d_age}\n"
    + f"Tasa de supervivencia general: {superv_rate}\n"
    + f"Tasa de supervivencia hombres: {superv_rate_male}\n"
    + f"Tasa de supervivencia mujeres: {superv_rate_female}"
)
print(to_print)
print_to_file("datos.txt", to_print)


# 2da parte
print("\n2da Parte")
print("1- Construir un intervalo de confianza, con confianza 95 %, para la edad promedio de las personas en el barco.")
std_d_div_n = standard_d_age / number_of_rows
print("Intervalo de confianza")
intervalo_confianza = (
    float(mean_age + 1.96 * std_d_div_n),
    float(mean_age - (1.96 * std_d_div_n)),
)
print(intervalo_confianza)
print("\n2- A partir de los datos de la muestra, con una certeza del 95 %")
print("¿Es posible afirmar que el promedio de edad de las mujeres interesadas en abordar el Titanik es mayor a 56 años?")
print("¿Es posible afirmar lo mismo para los hombres?"
female_ages = titanik_dataframe.loc[titanik_dataframe["gender"] == "female"]["age"]
male_ages = titanik_dataframe.loc[titanik_dataframe["gender"] == "male"]["age"]
print("Como se quiere manejar una certeza del 95%, entonces nuestro alpha valdría 1 - 95% = 0.05")
print("La hipotesis se rechaza si el pvalue es menor a 0.05")
stat_female, pvalue_female = stats.ttest_1samp(female_ages, 56, alternative="greater")
stat_male, pvalue_male = stats.ttest_1samp(male_ages, 56, alternative="greater")

print("\nValor P para si son mayores a 56, en promedio")
print(f"Mujer: {pvalue_female}")
print(f"Hombre: {pvalue_male}")
if pvalue_female < 0.05:
    print("No es posible afirmarlo para las mujeres")
else:
    print("Es posible afirmarlo para las mujeres")
if pvalue_male < 0.05:
    print("No es posible afirmarlo para los hombres")
else:
    print("Es posible afirmarlo para los hombres")


print("\n3- A partir de los datos de la muestra, con una certeza del 99 %")
print("¿Existe una diferencia significativa en la tasa de supervivencia entre hombres y mujeres?")


surv_male = titanik_dataframe[titanik_dataframe["gender"] == "female"]["survived"]
surv_female = titanik_dataframe[titanik_dataframe["gender"] == "male"]["survived"]
len_surv_male = len(surv_male)
len_surv_female = len(surv_female)
len_total = 0
# El método necesita que tengan la misma cantidad de elementos, así que reduzco al que tenga menor cantidad
if len_surv_female <= len_surv_male:
    len_total = len_surv_female
else:
    len_total = len_surv_male


statistic, pvalue_genders = stats.ttest_ind(
    surv_female[0:len_total], surv_male[0:len_total]
)
print("Valor p de diferencia entre promedio de edad por género")
print(pvalue_genders)
if pvalue_genders < 0.01:
    print("Existe una diferencia significativa entre hombres y mujeres")
else:
    print("No existe una diferencia significativa entre hombres y mujeres")

print("\n¿Existe una diferencia significativa en la tasa de supervivencia en las distintas clases?")
surv_first_class = titanik_dataframe[titanik_dataframe["p_class"] == 1]["survived"]
surv_sec_class = titanik_dataframe[titanik_dataframe["p_class"] == 2]["survived"]
surv_third_class = titanik_dataframe[titanik_dataframe["p_class"] == 3]["survived"]
len_first = len(surv_first_class)
len_sec = len(surv_sec_class)
len_third = len(surv_third_class)
len_total = 0
if len_first <= len_sec:
    len_total = len_first
else:
    len_total = len_sec

statistic, pvalue_classes_first_sec = stats.ttest_ind(
    surv_first_class[0:len_total],
    surv_sec_class[0:len_total],
)
if len_first <= len_third:
    len_total = len_first
else:
    len_total = len_third

statistic, pvalue_classes_first_third = stats.ttest_ind(
    surv_first_class[0:len_total],
    surv_third_class[0:len_total],
)
if len_sec <= len_third:
    len_total = len_sec
else:
    len_total = len_third

statistic, pvalue_classes_sec_third = stats.ttest_ind(
    surv_third_class[0:len_total],
    surv_sec_class[0:len_total],
)

print("Valores p de diferencia entre promedios por clases")
print("Primera vs segunda")
print(pvalue_classes_first_sec)
print("Segunda vs tercera")
print(pvalue_classes_sec_third)
print("Primera vs tercera")
print(pvalue_classes_first_third)
if pvalue_classes_first_sec > 0.01:
    print("Hay una diferencia significativa entre la primera y segunda clase")
else:
    print("No hay una diferencia significativa entre la primera y segunda clase")

if pvalue_classes_sec_third > 0.01:
    print("Hay una diferencia significativa entre la segunda y tercera clase")
else:
    print("No hay una diferencia significativa entre la segunda y tercera clase")

if pvalue_classes_first_third > 0.01:
    print("Hay una diferencia significativa entre la primera y tercera clase")
else:
    print("No hay una diferencia significativa entre la segunda y tercera clase")


print("\n4- A partir de los datos de la muestra, con una certeza del 95 %")
print("¿Es posible afirmar que en promedio las mujeres eran más jóvenes que los hombres en el barco?")
# Utilizando less, para que el valor p responda a si son
statistic, pvalue_ages = stats.ttest_ind(female_ages, male_ages, alternative="less")
print(f"Valor p para diferencia entre promedios {pvalue_ages}")
print(
    "Es posible afirmar que las mujeres eran en promedio más jovenes que los hombres?"
)
if pvalue_ages < 0.05:
    print("En promedio, no podemos afirmarlo")
else:
    print("En promedio, podemos afirmarlo")
